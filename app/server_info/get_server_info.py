import paramiko # type: ignore


def get_server_info(server):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # For testing only
        # ssh_client.connect(ip_addr, port, username, str(password))
        ssh_client.connect(server.server_ip, 22, server.username, server.password)

        from .cmd_list import server_info
        cmd = ''
        for info in server_info:
            cmd += info['name']
            cmd += info['cmd']

        stdin, stdout, stderr = ssh_client.exec_command(cmd)

        # Read the stream ONCE and store the content.
        full_output = stdout.read().decode()
        # To get a list of lines, split the stored string.
        output_lines = full_output.splitlines()

        error_output = stderr.read().decode()
        if error_output:
            print(error_output)
        return output_lines
    except Exception as e:
        print(f"연결 실패: {e}")
    finally:
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()