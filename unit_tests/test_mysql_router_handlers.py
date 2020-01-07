# Copyright 2018 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

import charm.openstack.mysql_router as mysql_router
import reactive.mysql_router_handlers as handlers

import charms_openstack.test_utils as test_utils


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        defaults = [
            "config.changed",
            "update-status",
            "upgrade-charm",
            "charm.installed"]
        hook_set = {
            "when": {
                "db_router_request": (
                    "db-router.connected", "charm.installed",),
                "bootstrap_mysqlrouter": (
                    mysql_router.DB_ROUTER_AVAILABLE, "charm.installed",),
                "start_mysqlrouter": (
                    mysql_router.MYSQL_ROUTER_BOOTSTRAPPED,
                    mysql_router.DB_ROUTER_AVAILABLE, "charm.installed",),
                "proxy_shared_db_requests": (
                    mysql_router.MYSQL_ROUTER_STARTED,
                    mysql_router.DB_ROUTER_AVAILABLE,
                    "shared-db.available",),
                "proxy_shared_db_responses": (
                    mysql_router.MYSQL_ROUTER_STARTED,
                    mysql_router.DB_ROUTER_PROXY_AVAILABLE,
                    "shared-db.available",),
            },
            "when_not": {
                "bootstrap_mysqlrouter": (
                    mysql_router.MYSQL_ROUTER_BOOTSTRAPPED,),
                "start_mysqlrouter": (
                    mysql_router.MYSQL_ROUTER_STARTED,),
            },
        }
        # test that the hooks were registered via the
        # reactive.mysql_router_handlers
        self.registered_hooks_test_helper(handlers, hook_set, defaults)


class TestMySQLRouterHandlers(test_utils.PatchHelper):

    def setUp(self):
        super().setUp()
        self.patch_release(
            mysql_router.MySQLRouterCharm.release)

        self.mr = mock.MagicMock()
        self.mr.db_prefix = "mysqlrouter"

        self.patch_object(handlers.charm, "provide_charm_instance",
                          new=mock.MagicMock())
        self.provide_charm_instance().__enter__.return_value = (self.mr)
        self.provide_charm_instance().__exit__.return_value = None

        self.shared_db = mock.MagicMock()
        self.db_router = mock.MagicMock()

    def test_db_router_request(self):
        handlers.db_router_request(self.db_router)
        self.db_router.set_prefix.assert_called_once_with(self.mr.db_prefix)

    def test_bootstrap_mysqlrouter(self):
        handlers.bootstrap_mysqlrouter(self.db_router)
        self.mr.bootstrap_mysqlrouter.assert_called_once()

    def test_start_mysqlrouter(self):
        handlers.start_mysqlrouter(self.db_router)
        self.mr.start_mysqlrouter.assert_called_once()

    def test_proxy_shared_db_requests(self):
        handlers.proxy_shared_db_requests(self.shared_db, self.db_router)
        self.mr.proxy_db_and_user_requests.assert_called_once_with(
            self.shared_db, self.db_router)

    def test_proxy_shared_db_responses(self):
        handlers.proxy_shared_db_responses(self.shared_db, self.db_router)
        self.mr.proxy_db_and_user_responses.assert_called_once_with(
            self.db_router, self.shared_db)
