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
    # GET: exibe o formulário limpo ou com resultado passado por querystring (após PRG)
    if request.method == 'GET':
        imc = request.args.get('imc', None)
        categoria = request.args.get('categoria', None)
        peso_ideal = request.args.get('peso_ideal', None)
        erro = request.args.get('erro', None)
        return render_template('index.html', imc=imc, categoria=categoria, peso_ideal=peso_ideal, erro=erro)

    # POST
    imc = request.args.get('imc')
    categoria = request.args.get('categoria')
    peso_ideal = request.args.get('peso_ideal')
    erro = request.args.get('erro')

    # POST: processa os dados do formulário
    try:
        # Não use variáveis antes de definir (corrige o problema da linha 19)
        peso_str = request.form.get('peso', '').replace(',', '.')
        altura_str = request.form.get('altura', '').replace(',', '.')
        crianca = request.form.get('crianca')

        peso = float(peso_str) if peso_str else 0.0
        altura = float(altura_str) if altura_str else 0.0

        if peso <= 0 or altura <= 0:
            # Em caso de erro, redireciona para GET com mensagem (PRG)
            return redirect(url_for('index', erro="Peso e altura devem ser valores positivos."))

        # Se houver lógica específica para 'crianca', trate aqui. Caso contrário, segue cálculo padrão.
        imc = peso / (altura ** 2)

        if imc < 16:
            categoria = "Magreza (Desnutrição)"
        elif imc < 16.9:
            categoria = "Magreza (Moderada)"
        elif imc < 18.5:
            categoria = "Magreza (Leve)"
        elif imc < 25:
            categoria = "Peso normal"
        elif imc < 30:
            categoria = "Sobrepeso"
        elif imc < 35:
            categoria = "Obesidade I"
        elif imc < 40:
            categoria = "Obesidade II (Severa)"
        else:
            categoria = "Obesidade III (Mórbida)"

        peso_ideal = 22 * (altura ** 2)

        # PRG: redireciona para GET na mesma rota, evitando reenvio do formulário
        # e “persistência” indesejada ao atualizar a página.
        return redirect(url_for('index',
                                imc=f"{imc:.2f}",
                                categoria=categoria,
                                peso_ideal=f"{peso_ideal:.2f}",
                                erro=None))
    except ValueError:
        return redirect(url_for('index', erro="Informe números válidos (use ponto ou vírgula para decimais)."))


# Ponto de entrada da aplicação.
# Executa o servidor de desenvolvimento do Flask com:
# - host: endereço local (loopback)
# - port: porta (inteiro)
# - debug=True: recarrega automaticamente e mostra tracebacks detalhados
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)