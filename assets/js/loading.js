if (document.getElementById("minha-pagina-carregamento")) {
    function checkServer() {
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                // Verifica se o servidor está pronto pela análise do conteúdo, não apenas pelo status
                if (xhr.status === 200) {
                    // Verifica se a resposta contém o conteúdo da aplicação e não da página de loading
                    if (!xhr.responseText.includes("Obrigado pela paciência!")) {
                        window.location.reload();
                    } else {
                        // Se ainda é a página de loading, tenta novamente após 5 segundos
                        setTimeout(checkServer, 5000);
                    }
                } else {
                    // Se houver erros como 502, 503 ou 504, tenta novamente após 5 segundos
                    setTimeout(checkServer, 5000);
                }
            }
        };

        xhr.open('GET', '/', true);
        xhr.send();
    }

    checkServer();
}
