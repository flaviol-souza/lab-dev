$(document).ready(function(){
    $.ajax({
        dataType: "xml",
        url: "http://servicos.cptec.inpe.br/XML/cidade/244/previsao.xml"
    }). then(function(data){
        $(data).find("cidade").each(function () {
            var _name = 'cidade: ' + $(this).find('nome').text();
            $('.nome').append(_name);

            var _uf = 'Estado: ' + $(this).find('uf').text();
            $('.uf').append(_uf);
        });
    })
});