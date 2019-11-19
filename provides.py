#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class ClusterDNSProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:cluster-dns}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.joined')

    @hook('{provides:cluster-dns}-relation-changed')
    def changed(self):
        if self.get_ip():
            self.set_state('{relation_name}.ready')
        else:
            self.remove_state('{relation_name}.ready')

    @hook('{provides:cluster-dns}-relation-{broken,departed}')
    def broken_departed(self):
        self.remove_state('{relation_name}.ready')
        self.remove_state('{relation_name}.joined')

    @hook('{provides:cluster-dns}-relation-broken')
    def broken(self):
        self.set_state('{relation_name}.removed')

    def get_ip(self):
        """Return the Cluster DNS IP.
        """
        for conv in self.conversations():
            host = conv.get_remote('host') or conv.get_remote(
                'private-address')

            return host
        return False

    def send_domain(self, domain):
        conv = self.conversation()
        conv.set_remote('domain', domain)
