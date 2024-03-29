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


class ClusterDNSRequires(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:cluster-dns}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')

    @hook('{requires:cluster-dns}-relation-changed')
    def changed(self):
        conv = self.conversation()
        if self.get_domain():
            conv.set_state('{relation_name}.domain-ready')
        else:
            conv.remove_state('{relation_name}.domain-ready')

    @hook('{requires:cluster-dns}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.ready')
        conv.remove_state('{relation_name}.joined')

    def send_ip(self, host):
        conv = self.conversation()
        conv.set_remote('host', host)

    def get_domain(self):
        """Return the Cluster DNS Domain.
        """
        for conv in self.conversations():
            domain = conv.get_remote('domain')

            return domain
