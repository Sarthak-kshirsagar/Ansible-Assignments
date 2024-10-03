#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os

def manage_nginx(action):
    """
    Manage NGINX service based on the action specified.
    """
    if action == "install":
        cmd = "yum install -y nginx"
    elif action == "start":
        cmd = "systemctl start nginx"
    elif action == "restart":
        cmd = "systemctl restart nginx"
    else:
        return False, "Invalid action specified."

    
    rc = os.system(cmd)

    
    if rc == 0:
        return True, f"NGINX has been successfully {action}ed."
    else:
        return False, f"Failed to {action} NGINX service."

def run_module():
    # module arguments
    module_args = dict(
        action=dict(type='str', required=True, choices=['install', 'start', 'restart'])
    )

    # Result dictionary
    result = dict(
        changed=False,
        message=''
    )

    # Creating the Ansible module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    
    action = module.params['action']

    # If in check mode, return the result
    if module.check_mode:
        module.exit_json(**result)

    
    changed, message = manage_nginx(action)
    result['changed'] = changed
    result['message'] = message

    # Exit the module
    if changed:
        module.exit_json(**result)
    else:
        module.fail_json(msg=message)

if __name__ == '__main__':
    run_module()

