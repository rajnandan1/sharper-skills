A storage service client got a new feature behind a feature flag. The feature opens mTLS connections from the client to the storage service and includes new certificate-reload logic on both client and server, meant to avoid using an expired certificate. The server flag was enabled first with no visible change. Then the client flag was enabled on the smallest client deployment, about 5,000 hosts in one data center.

Within about 10 minutes of enabling the client flag, client-side p99 latency to the storage service rose sharply, and server-side p99 latency rose at the same time. Error rate and request rate did not change. The pre-production environment ran the same build with the flag on and showed no latency change. Pre-production runs 2 shards with 1 replica each. Production runs 5 shards with 80 replicas each.

Measurements already taken on one production client host:
- With the flag on (client and server), the client's DNS lookup for the storage service returns about 400 addresses.
- With the flag off on the client and pointed at a storage deployment with the flag off, the same lookup returns about 5 addresses.
- TLS handshake time to the server, measured with tcpdump, is the same in both configurations, a few tens of milliseconds.

Produce, as markdown: the numbered fact list with sources, the control and variable, the signal and noise tagging, the hypotheses-by-fact matrix with every plausible hypothesis as a row, the strongest signal and why it is strong, the winning row, the reviewer answers, and the fix with the regression test. Every claim must cite a fact number. If the facts do not single out one row, say so and list the ? facts to gather next in order of cost.
