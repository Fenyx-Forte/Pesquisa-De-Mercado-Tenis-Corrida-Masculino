if (document.getElementById("minha-pagina-carregamento")) {
    function checkServer() {
        const xhr = new XMLHttpRequest();
        const method = "GET";
        const url = "/";

        xhr.open(method, url, true);

        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                const status = xhr.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    const conteudo = xhr.responseText;
                    if (conteudo.includes("Aguarde alguns instantes")){
                        setTimeout(checkServer, 5000);
                    } else{
                        window.location.reload();
                    }
                } else {
                    setTimeout(checkServer, 5000);
                }
            }
        };

        xhr.send();
    }

    checkServer();
}
