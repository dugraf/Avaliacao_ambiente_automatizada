import winrm

def conectar_servidor_winrm(ip, usuario, senha):
    try:
        session = winrm.Session(ip, auth=(usuario, senha))
        response = session.run_cmd('ipconfig')
        if response.status_code == 0:
            print(response.std_out.decode('utf-8'))
            return True
        else:
            print(f"Erro na conexão: {response.std_err.decode('utf-8')}")
            return False
    except Exception as e:
        print(f"⚠️ Falha na conexão WinRM: {e}")
        return False
