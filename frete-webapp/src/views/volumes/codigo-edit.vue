<script setup>
import { useRoute, useRouter } from 'vue-router'
import { doc } from 'firebase/firestore'
import { useDocument } from 'vuefire'
import { db, getdoc } from '@/backend/index'
import { onBeforeMount, onMounted, ref } from 'vue'
import QRCode from '@/components/QRCode.vue'
import moment from 'moment'

const route = useRoute()
const router = useRouter()
const codigo = route.params.codigo
const {
  // rename the Ref to something more meaningful
  data: volume,
  // is the subscription still pending?
  pending,
  // did the subscription fail?
  error,
  // A promise that resolves or rejects when the initial state is loaded
  promise
} = useDocument(doc(db, "volumes", codigo))

const responsavel = ref(null)

function print(){
  window.print()
}

</script>
<template>
  <!-- Carregando -->
  <div v-if="pending" class="d-flex justify-content-center">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <template v-else>
    <!-- Carregou -->
    <template v-if="!volume || volume.deleted">
      <!-- Não existe -->
      <div class="row justify-content-start g-3">
        <div class="col alert alert-danger">
          <p class="text-center fs-3">O volume pesquisado não existe!</p>
          <p class="text-center">
            <RouterLink :to="{ name: 'volumes' }"><i class="bi bi-arrow-left"></i> Voltar</RouterLink>
          </p>
        </div>
      </div>
    </template>
    <template v-else>
      <!-- Existe -->

      <div class="row justify-content-start g-3">
        <div class="col-8">
          <h3>Volume {{ volume.codigo }}</h3>
          <p class="mb-1"><b>Responsável:</b> {{ volume.responsavel.nome }}</p>
          <p class="mb-1"><b>Origem:</b> {{ volume.origem.ambiente_codigo }} &dash; {{ volume.origem.ambiente_nome }}</p>
          <p class="mb-1"><b>Criado em:</b> {{ moment.unix(volume.data_criacao.seconds).format("DD/MM/YY HH:MM") }}</p>
          <p class="mb-1"><b>Local atual:</b> {{ volume.localizacao_atual.ambiente_codigo }}</p>
          <p class="mb-1"><b>Destino:</b> </p>
        </div>

        <div class="col d-flex justify-content-end">
          <QRCode :path="route.fullPath"></QRCode>
        </div>

      </div>
      <div class="row">
        <div class="col">
          <p class="fw-bold">Lista de itens</p>
          <ul class="list-group">
            <li class="list-group-item justify-content-between d-flex" v-for="item in volume.items">
              <span>
                {{ item.descricao ? item.descricao : item.short_descricao }}
              </span>
              <span class="bagde text-secondary">{{ item.key }}</span>
            </li>
          </ul>

          <p @click="print" role="button" class="d-print-none mt-4 form-text text-end">Essa página foi otimizada para impressão. Clique aqui para imprimir <i class="bi bi-printer"></i>.</p>
        </div>
      </div>

    </template>
  </template>
</template>
<style>
.text-elipse {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.codigo-span {
  min-width: 4.5em;
  max-width: 6em;
}
</style>