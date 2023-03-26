# Findings

Realized reached search wasn't actually being called
In trying to implement reached, comparing the state drastically slowed down search
Turns out I was performing the hash for state EACH time rather than once and adding it
Once reached became an array of hashes instead of nodes, reached worked great compared to not using it


Max frontier length is enormous, in the 10s of thousands depending on depth
With a depth of 500 and reached enabled, 65-70k nodes are places on reached
Limiting the frontier size drastically decreases the ending result, but it does speed things up...
