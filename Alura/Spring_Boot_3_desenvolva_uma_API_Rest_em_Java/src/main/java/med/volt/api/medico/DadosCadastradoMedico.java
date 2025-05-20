package med.volt.api.medico;

import med.volt.api.endereco.DadosEndereco;

public record DadosCadastradoMedico(String nome, String email, String crm, Especialidade especialidade, DadosEndereco endereco)  {

}
