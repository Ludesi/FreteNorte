<script setup>
import { useAmbientesUserStore } from '@/stores/ambientes';
import { useUserPermissionsStore } from '@/stores/user';
import { RouterLink } from 'vue-router';
import { computed, ref, reactive, onMounted, onServerPrefetch, watch } from 'vue'; 
import { usePendingPromises } from 'vuefire';   
 
const permissions = useUserPermissionsStore()


const meus_ambientes = useAmbientesUserStore()
 
meus_ambientes.update_stats()
 
</script>

<template>
    <div class="row my-3">
        <div class="col">
            <h1>SisLog Norte</h1>
            <p> Sistema de controle da logística da mudança do campus Blumenau.</p>
            <h2>Seus ambientes</h2>
            <div class="my-3">
                <div class="card my-2" v-for="(x, i) in meus_ambientes.dados">
                    <div class="card-body" v-if="x">
                        <h5 class="card-title">{{ x.ambiente_codigo }}</h5>
                        <h6 class="card-subtitle mb-2 text-body-secondary">{{ x.ambiente_nome }}</h6>
                        <p class="card-text">
                        <div v-if="meus_ambientes.status[x.ambiente_codigo]" class="progress" role="progressbar" aria-label="Default striped example"
                            :aria-valuenow="meus_ambientes.status[x.ambiente_codigo].volumados" aria-valuemin="0" :aria-valuemax="meus_ambientes.status[x.ambiente_codigo].todos">
                            <div class="progress-bar progress-bar-striped" :style="{ width: meus_ambientes.status[x.ambiente_codigo].percent + '%' }">
                                {{  meus_ambientes.status[x.ambiente_codigo].volumados }} de {{ meus_ambientes.status[x.ambiente_codigo].todos }} volumados</div> 
                        </div>
                        </p>
                        <RouterLink :to="{ name: 'items-ambiente', params: { ambiente: x.ambiente_codigo } }">Ver ambiente
                        </RouterLink>
                    </div>
                </div>


            </div>

        </div>
    </div>
</template>
