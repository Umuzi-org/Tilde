kubectl exec --stdin --tty tilde-rabbitmq-rabbitmq-0 -- /bin/bash
rabbitmqctl list_queues

rabbitmqctl purge_queue default.DQ




```
Help:

   help                          Displays usage information for a command
   version                       Displays CLI tools version

Nodes:

   await_startup                 Waits for the RabbitMQ application to start on the target node
   reset                         Instructs a RabbitMQ node to leave the cluster and return to its virgin state
   rotate_logs                   Instructs the RabbitMQ node to perform internal log rotation
   shutdown                      Stops RabbitMQ and its runtime (Erlang VM). Monitors progress for local nodes. Does not require a PID file path.
   start_app                     Starts the RabbitMQ application but leaves the runtime (Erlang VM) running
   stop                          Stops RabbitMQ and its runtime (Erlang VM). Requires a local node pid file path to monitor progress.
   stop_app                      Stops the RabbitMQ application, leaving the runtime (Erlang VM) running
   wait                          Waits for RabbitMQ node startup by monitoring a local PID file. See also 'rabbitmqctl await_online_nodes'

Cluster:

   await_online_nodes            Waits for <count> nodes to join the cluster
   change_cluster_node_type      Changes the type of the cluster node
   cluster_status                Displays all the nodes in the cluster grouped by node type, together with the currently running nodes
   force_boot                    Forces node to start even if it cannot contact or rejoin any of its previously known peers
   force_reset                   Forcefully returns a RabbitMQ node to its virgin state
   forget_cluster_node           Removes a node from the cluster
   join_cluster                  Instructs the node to become a member of the cluster that the specified node is in
   rename_cluster_node           Renames cluster nodes in the local database
   update_cluster_nodes          Instructs a cluster member node to sync the list of known cluster members from <seed_node>

Replication:

   cancel_sync_queue             Instructs a synchronising mirrored queue to stop synchronising itself
   sync_queue                    Instructs a mirrored queue with unsynchronised mirrors (follower replicas) to synchronise them

Users:

   add_user                      Creates a new user in the internal database
   authenticate_user             Attempts to authenticate a user. Exits with a non-zero code if authentication fails.
   change_password               Changes the user password
   clear_password                Clears (resets) password and disables password login for a user
   delete_user                   Removes a user from the internal database. Has no effect on users provided by external backends such as LDAP
   list_users                    List user names and tags
   set_user_tags                 Sets user tags

Access Control:

   clear_permissions             Revokes user permissions for a vhost
   clear_topic_permissions       Clears user topic permissions for a vhost or exchange
   list_permissions              Lists user permissions in a virtual host
   list_topic_permissions        Lists topic permissions in a virtual host
   list_user_permissions         Lists permissions of a user across all virtual hosts
   list_user_topic_permissions   Lists user topic permissions
   list_vhosts                   Lists virtual hosts
   set_permissions               Sets user permissions for a vhost
   set_topic_permissions         Sets user topic permissions for an exchange

Monitoring, observability and health checks:

   environment                   Displays the name and value of each variable in the application environment for each running application
   list_bindings                 Lists all bindings on a vhost
   list_channels                 Lists all channels in the node
   list_ciphers                  Lists cipher suites supported by encoding commands
   list_connections              Lists AMQP 0.9.1 connections for the node
   list_consumers                Lists all consumers in a vhost
   list_exchanges                Lists exchanges
   list_hashes                   Lists hash functions supported by encoding commands
   list_queues                   Lists queues and their properties
   list_unresponsive_queues      Tests queues to respond within timeout. Lists those which did not respond
   node_health_check             Performs several opinionated health checks of the target node
   ping                          Checks that the node OS process is up, registered with EPMD and CLI tools can authenticate with it
   report                        Generate a server status report containing a concatenation of all server status information for support purposes
   schema_info                   Lists schema database tables and their properties
   status                        Displays broker status information

Parameters:

   clear_global_parameter        Clears a global runtime parameter
   clear_parameter               Clears a runtime parameter.
   list_global_parameters        Lists global runtime parameters
   list_parameters               Lists runtime parameters for a virtual host
   set_global_parameter          Sets a runtime parameter.
   set_parameter                 Sets a runtime parameter.

Policies:

   clear_operator_policy         Clears an operator policy
   clear_policy                  Clears (removes) a policy
   list_operator_policies        Lists operator policy overrides for a virtual host
   list_policies                 Lists all policies in a virtual host
   set_operator_policy           Sets an operator policy that overrides a subset of arguments in user policies
   set_policy                    Sets or updates a policy

Virtual hosts:

   add_vhost                     Creates a virtual host
   clear_vhost_limits            Clears virtual host limits
   delete_vhost                  Deletes a virtual host
   list_vhost_limits             Displays configured virtual host limits
   restart_vhost                 Restarts a failed vhost data stores and queues
   set_vhost_limits              Sets virtual host limits
   trace_off                     
   trace_on                      

Node configuration:

   decode                        Decrypts an encrypted configuration value
   encode                        Encrypts a sensitive configuration value
   set_cluster_name              Sets the cluster name
   set_disk_free_limit           Sets the disk_free_limit setting
   set_log_level                 Sets log level in the running node
   set_vm_memory_high_watermark  Sets the vm_memory_high_watermark setting

Operations:

   close_all_connections         Instructs the broker to close all connections for the specified vhost or entire RabbitMQ node
   close_connection              Instructs the broker to close the connection associated with the Erlang process id
   eval                          Evaluates a snippet of Erlang code on the target node
   exec                          Evaluates a snippet of Elixir code on the CLI node
   force_gc                      Makes all Erlang processes on the target node perform/schedule a full sweep garbage collection
   hipe_compile                  Only exists for backwards compatibility. HiPE support has been dropped starting with Erlang 22. Do not use

Queues:

   delete_queue                  Deletes a queue
   purge_queue                   Purges a queue (removes all messages in it)

Other:

   enable_feature_flag           
   list_feature_flags    
```