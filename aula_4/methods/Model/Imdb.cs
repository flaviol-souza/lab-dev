namespace methods.Model;

public class Imdb {

    public Imdb(){}

    public Imdb(int id, String titulo, int ano){
        Id = id;
        Titulo = titulo;
        AnoLancamento = ano;
    }
    public int Id {get; set;}
    public String? Titulo {get; set;}    
    public int AnoLancamento {get; set;}
    public double Nota {get; set;}

}