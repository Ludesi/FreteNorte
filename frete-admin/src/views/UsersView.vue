<script setup>
import UserRole from '../components/UserRole.vue';
import Modal from '../components/Modal.vue';
import UserAmbientes from '../components/UserAmbientes.vue';
import { ref, computed } from 'vue';
import { useUsuariosStore } from '../stores/users';
import { useListaAmbientes } from '../stores/agregados';

const usuarios = useUsuariosStore()
const selectmail = ref(false)
const lista_ambientes = useListaAmbientes()

const user_edit = computed(() => {
    if (selectmail.value && usuarios.usuarios) {
        return usuarios.usuarios[selectmail.value]
    } else {
        return { nome: "", email: "", role: "", ambientes: [], usuario_de: [] }
    }
})

function update_role(email, role) {
    usuarios.usuarios[email].role = role
}


function add_lider_ambiente(email, ambiente) {
    usuarios.usuarios[email].ambientes.push(ambiente)
    usuarios.edit_array.push(["add_lider", email, ambiente])
}

function add_user_ambiente(email, ambiente) {
    usuarios.usuarios[email].usuario_de.push(ambiente)
    usuarios.edit_array.push(["add_user", email, ambiente])
}



function remove_lider_ambiente(email, ambiente) {
    const filtrado = usuarios.usuarios[email].ambientes.filter(x => x !== ambiente)
    usuarios.usuarios[email].ambientes = filtrado
    usuarios.edit_array.push(["remove_lider", email, ambiente])
}


function remove_user_ambiente(email, ambiente) {
    const filtrado = usuarios.usuarios[email].usuario_de.filter(x => x !== ambiente)
    usuarios.usuarios[email].usuario_de = filtrado
    usuarios.edit_array.push(["remove_user", email, ambiente])
}


async function update_user(email) {
    const referencia = usuarios.usuarios[email]
    const uptime = await usuarios.update_user(referencia)
    return true
}

const pesquisa_usuario = ref(null)

const usuarios_filtrados = computed(() => {
    const lista_usuarios = Object.values(usuarios.usuarios)
    if (pesquisa_usuario.value) {
        const regex = new RegExp(`.*${pesquisa_usuario.value}.*`, 'i')
        const filtrado = lista_usuarios.filter(elem => regex.test(elem.nome) || regex.test(elem.email))
        return filtrado
    } else {
        return lista_usuarios
    }

})

</script>
<template>
    <Modal modalid="BossaModal" :salve_callback="async () => await update_user(user_edit.email)">
        <template #titulo>Editar usuário</template>
        <template #corpo>
            <div class="mb-3">
                <label for="nome" class="form-label">Nome</label>
                <input :value="user_edit.nome" type="text" class="form-control" id="nome" disabled>
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">e-mail</label>
                <input :value="user_edit.email" type="text" class="form-control" id="email" disabled>
            </div>

            <div class="mb-3">
                <label for="perfil" class="form-label">Perfil</label>
                <UserRole id="perfil" :role="user_edit.role" label="Perfil"
                    @updaterole="(x) => update_role(user_edit.email, x)"></UserRole>
            </div>

            <div class="mb-3">
                <label for="ambientes" class="form-label">Líder dos seguintes ambientes</label>
                <UserAmbientes 
                    @remove="(x) => remove_lider_ambiente(user_edit.email, x)"
                    @add="(x) => add_lider_ambiente(user_edit.email, x)" 
                    :selected="user_edit.ambientes"
                    :all="lista_ambientes.todos"
                    :unselectable="lista_ambientes.liderados"
                    ></UserAmbientes>
            </div>

            <div class="mb-3">
                <label for="ambientes" class="form-label">Usuário dos seguintes ambientes</label>
                <UserAmbientes 
                    @remove="(x) => remove_user_ambiente(user_edit.email, x)"
                    @add="(x) => add_user_ambiente(user_edit.email, x)" 
                    :selected="user_edit.usuario_de"
                    :all="lista_ambientes.todos"
                    :unselectable="[]"
                    ></UserAmbientes>
            </div>
        </template>
    </Modal>
    <table class="table">
        <thead>
            <tr>
                <th>Nome</th>
                <th>e-mail</th>
                <th>Perfil</th>
                <th>Ambientes</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td colspan="5"><input v-model="pesquisa_usuario" placeholder="Digite para pesquisar" class="form-control">
                </td>
            </tr>
            <tr v-for="(user, index) in usuarios_filtrados">
                <td> {{ user.nome }} </td>
                <td> <code>{{ user.email }}</code> </td>
                <td> {{ user.role }} </td>
                <td> 
                    <span :title="'Líder do ambiente ' + x" class="badge text-bg-primary m-1" v-for="x in user.ambientes">{{ x }}</span>
                    <span :title="'Usuário do ambiente ' + x " class="badge text-bg-secondary m-1" v-for="x in user.usuario_de">{{ x }}</span>
                </td>
                <td> <button title="Editar usuário" class="btn btn-secondary no-wrap" data-bs-target="#BossaModal"
                        data-bs-toggle="modal" @click="() => selectmail = user.email"><i class="bi bi-pencil"></i></button>
                </td>
            </tr>
        </tbody>
    </table>
</template>