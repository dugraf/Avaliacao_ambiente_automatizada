Instruções de Instalação e Manutenção
Este projeto requer a instalação de alguns componentes específicos para funcionar corretamente. Siga os passos abaixo para configurar o ambiente de desenvolvimento.

1. Instalar as Ferramentas de Compilação C++
    Para garantir que o projeto seja construído e funcione corretamente, você precisa instalar o Microsoft Visual C++ Build Tools. Esses pacotes são necessários para compilar bibliotecas nativas, como o psutil, que dependem de extensões C++.

    Passos para Instalar o Visual C++ Build Tools:
    Acesse o link abaixo para baixar o instalador do Microsoft Visual C++ Build Tools:

    Visual C++ Build Tools
    Execute o arquivo vs_BuildTools.exe que você acabou de baixar.

    Durante a instalação, marque a opção:

    "Desktop development with C++".
    Essa opção inclui:
    Compilador C++ (cl.exe).
    Ferramentas de construção como MSBuild e CMake.
    SDK do Windows necessário para a compilação de pacotes nativos.
    Após selecionar a opção, clique em "Instalar" e aguarde até que a instalação seja concluída.

    Após a Instalação:
    Reinicie o terminal: Após a instalação, feche e abra o terminal novamente para garantir que as novas ferramentas estejam corretamente disponíveis no seu sistema.

2. Instalar Dependências do Projeto
    Com as ferramentas de compilação C++ instaladas, o próximo passo é instalar as dependências necessárias para o projeto.

    Certifique-se de que você tenha o Python 3.x e o pip instalados em seu sistema. Você pode verificar isso com os seguintes comandos:
    python --version
    pip --version
    Navegue até o diretório onde o projeto está localizado.

    Execute o comando abaixo para instalar as dependências listadas no arquivo requisitos.txt:
    pip install -r requisitos.txt
    Isso instalará todas as bibliotecas necessárias para rodar o projeto, como o psutil, tk, entre outras.

python -m PyInstaller --onedir --noconsole --add-data "assets;assets" --add-data "logs;logs" --add-data "controllers\scripts;controllers\scripts" --add-binary "D:\Program Files\OpenSSL-Win64\bin\libssl-3-x64.dll;." --add-binary "D:\Program Files\OpenSSL-Win64\bin\libcrypto-3-x64.dll;." --hidden-import=asyncio --hidden-import=uuid --hidden-import=cryptography --hidden-import=cryptography.hazmat.backends --hidden-import=cryptography.hazmat.backends.openssl --hidden-import=cryptography.hazmat.bindings._rust --collect-submodules cryptography --additional-hooks-dir=hooks main.py