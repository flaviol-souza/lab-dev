$(document).ready(function(){
    $.ajax({
        dataType: "xml",
        url: "http://servicos.cptec.inpe.br/XML/listaCidades"
    }). then(function(data){
        console.log($(data))
        $(data).find("cidade").each(function () {
            $('#cidades').append($('<option>', {
                value: $(this).find('id').text(),
                text: $(this).find('nome').text() + '/' + $(this).find('uf').text()
            }));
        });
    })
});

function consultaPrevisao() {
    var val = $('#cidades').find(":selected").val();
    if(val == null || val == undefined || val === ''){
        alert("Selecione uma cidade!")
    } else {
        $.ajax({
            dataType: "xml",
            url: "http://servicos.cptec.inpe.br/XML/cidade/"+val+"/previsao.xml"
        }). then(function(data){
            $(data).find("cidade").each(function () {
                var _name = 'Cidade: ' + $(this).find('nome').text();
                $('#nome').append(_name);
    
                var _uf = 'Estado: ' + $(this).find('uf').text();
                $('#uf').append(_uf);  
            });

            var _dias = [];
            $(data).find("dia").each(function () {
                _dias.push($(this).text());
            });

            var _maxs = [];
            $(data).find("maxima").each(function () {
                _maxs.push($(this).text());
            });

            var _mins = [];
            $(data).find("minima").each(function () {
                _mins.push($(this).text());
            });

            var _tempos = [];
            $(data).find("tempo").each(function () {
                _tempos.push($(this).text());
            });

            for (let i = 0; i < _dias.length; i++) {
                $('#previsao ul').append('<li>'+_dias[i]+'</li>');
                $('#previsao ul').append('<p>'+'Min.: ' + _mins[i] + 'Cº - Max.: '+ _maxs[i] + 'Cº'+'</p>');
                $('#previsao ul').append('<p>'+getTempo(_tempos[i])+'</p>');
            }            
        });
    }
    
    function getTempo(sigla){
        var mapTempo = {
            "ec": "Encoberto com Chuvas Isoladas",
            "ci": "Chuvas Isoladas",
            "c": "Chuva",
            "in": "Instável",
            "pp": "Poss. de Pancadas de Chuva",
            "cm": "Chuva pela Manhã",
            "cn": "Chuva a Noite",
            "pt": "Pancadas de Chuva a Tarde",
            "pm": "Pancadas de Chuva pela Manhã",
            "np": "Nublado e Pancadas de Chuva",
            "pc": "Pancadas de Chuva",
            "pn": "Parcialmente Nublado",
            "cv": "Chuvisco",
            "ch": "Chuvoso",
            "t": "Tempestade",
            "ps": "Predomínio de Sol",
            "e": "Encoberto",
            "n": "Nublado",
            "cl": "Céu Claro",
            "nv": "Nevoeiro",
            "g": "Geada",
            "ne": "Neve",
            "nd": "Não Definido",
            "pnt": "Pancadas de Chuva a Noite",
            "psc": "Possibilidade de Chuva",
            "pcm": "Possibilidade de Chuva pela Manhã",
            "pct": "Possibilidade de Chuva a Tarde",
            "pcn": "Possibilidade de Chuva a Noite",
            "npt": "Nublado com Pancadas a Tarde",
            "npn": "Nublado com Pancadas a Noite",
            "ncn": "Nublado com Poss. de Chuva a Noite",
            "nct": "Nublado com Poss. de Chuva a Tarde",
            "ncm": "Nubl. c/ Poss. de Chuva pela Manhã",
            "npm": "Nublado com Pancadas pela Manhã",
            "npp": "Nublado com Possibilidade de Chuva",
            "vn": "Variação de Nebulosidade",
            "ct": "Chuva a Tarde",
            "ppn": "Poss. de Panc. de Chuva a Noite",
            "ppt": "Poss. de Panc. de Chuva a Tarde",
            "ppm": "Poss. de Panc. de Chuva pela Manhã"
          }

          return mapTempo[sigla];
    }
}