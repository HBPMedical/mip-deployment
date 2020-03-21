## Ports Configuration

If you want your MIP installation to be accessible externally you should open the following ports:
  - 80
  - 8095

If you use iptables, the configuration should be:
```
Input:
-A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A INPUT -p tcp -m tcp --sport 80 -j ACCEPT
Output:
-Α OUTPUT -p tcp -m tcp --dport 80 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 80 -j ACCEPT

Input:
-A INPUT -p tcp -m tcp --dport 8095 -j ACCEPT
-A INPUT -p tcp -m tcp --sport 8095 -j ACCEPT
Output:
-Α OUTPUT -p tcp -m tcp --dport 8095 -j ACCEPT
-A OUTPUT -p tcp -m tcp --sport 8095 -j ACCEPT