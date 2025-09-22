# Importa os utilitários do Flask:
# - Flask: para criar a aplicação
# - render_template: para renderizar templates Jinja2 (HTML)
# - request: para acessar dados enviados pelo formulário (POST)
# - redirect, url_for: para redirecionamentos entre rotas
from flask import Flask, render_template, request, redirect, url_for

# Instancia a aplicação Flask.
# Como a pasta padrão de templates se chama "templates", não é necessário configurar nada extra.
app = Flask(__name__)

# Define a rota principal "/" para aceitar tanto GET quanto POST.
# - GET: exibe a página com o formulário
# - POST: processa o envio do formulário e calcula o IMC
@app.route('/', methods=['GET', 'POST'])
def index():
    # Se o método for POST, processamos os dados submetidos pelo formulário
    if request.method == 'POST':
        erro = None  # variável para armazenar mensagens de erro (se houver)
        try:
            # Lê os campos enviados com o formulário.
            # Troca vírgula por ponto para permitir "1,75" além de "1.75".
            peso = float(request.form.get('peso', '').replace(',', '.'))
            altura = float(request.form.get('altura', '').replace(',', '.'))

            # Validação básica: não aceitar zero ou valores negativos.
            if peso <= 0 or altura <= 0:
                erro = "Peso e altura devem ser valores positivos."
            else:
                # Cálculo do IMC: peso (kg) dividido pela altura (m) ao quadrado.
                imc = peso / (altura ** 2)

                # Classificação segundo faixas usuais para adultos.
                if imc < 18.5:
                    categoria = "Abaixo do peso"
                elif imc < 25:
                    categoria = "Peso normal"
                elif imc < 30:
                    categoria = "Sobrepeso"
                elif imc < 35:
                    categoria = "Obesidade I"
                elif imc < 40:
                    categoria = "Obesidade II"
                else:
                    categoria = "Obesidade III"

                # Renderiza o template já com resultado e sem erro.
                return render_template('index.html', imc=imc, categoria=categoria, erro=None)

        except ValueError:
            # Captura erro de conversão (ex.: campo vazio ou texto inválido)
            erro = "Informe números válidos (use ponto ou vírgula para decimais)."

        # Em caso de erro de validação/conversão, renderiza template informando a mensagem.
        return render_template('index.html', imc=None, categoria=None, erro=erro)

    # Se for GET, apenas exibe a página inicial com variáveis nulas (sem resultado ainda).
    return render_template('index.html', imc=None, categoria=None, erro=None)

# Rota opcional "/home": faz um redirecionamento para a rota principal "/"
@app.route('/home')
def home():
    return redirect(url_for('index'))

# Ponto de entrada da aplicação.
# Executa o servidor de desenvolvimento do Flask com:
# - host: endereço local (loopback)
# - port: porta (inteiro)
# - debug=True: recarrega automaticamente e mostra tracebacks detalhados
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)