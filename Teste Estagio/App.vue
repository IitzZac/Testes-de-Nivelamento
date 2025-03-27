<template>
    <div class="container">
      <h1>Busca de Operadoras</h1>
      <input v-model="busca" @input="buscarOperadoras" placeholder="Digite o nome ou CNPJ" />
      
      <div v-if="operadoras.length">
        <h2>Resultados:</h2>
        <ul>
          <li v-for="operadora in operadoras" :key="operadora.cnpj">
            {{ operadora.razao_social }} - CNPJ: {{ operadora.cnpj }}
          </li>
        </ul>
      </div>
      
      <p v-else>Nenhuma operadora encontrada.</p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        busca: "",
        operadoras: []
      };
    },
    methods: {
      async buscarOperadoras() {
        if (this.busca.length > 2) {
          const response = await axios.get(`http://127.0.0.1:5000/operadoras?q=${this.busca}`);
          this.operadoras = response.data;
        } else {
          this.operadoras = [];
        }
      }
    }
  };
  </script>
  
  <style>
  .container {
    max-width: 600px;
    margin: auto;
    text-align: center;
  }
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
  }
  </style>
  