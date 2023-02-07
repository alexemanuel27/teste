import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

class Pessoa {
    public String nome;
    public String pais;

    public Pessoa(String nome, String pais) {
        this.nome = nome;
        this.pais = pais;
    }
}


public class App {
    public static void main(String[] args) throws Exception {

        Pessoa pessoa1 = new Pessoa("alex", "brazil");
        Pessoa pessoa2 = new Pessoa("alex", "brazil");
        Pessoa pessoa3 = new Pessoa("alex", "japao");

        List<Pessoa> pessoas = List.of(pessoa1, pessoa2, pessoa3);

        Map<String, Long> counts = 
            pessoas.stream().collect(Collectors.groupingBy(e -> e.pais, Collectors.counting()));

        System.out.println(counts);
    }
}
