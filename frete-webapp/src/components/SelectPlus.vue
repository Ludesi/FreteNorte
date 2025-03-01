<template>
    <div class="dropdown" v-if="options">
  
      <!-- Dropdown Input -->
      <input :class="classe" class="dropdown-input form-select"
        :name="name"
        @focus="showOptions()"
        @blur="exit()"
        @keyup="keyMonitor"
        v-model="searchFilter"
        :disabled="disabled"
        :placeholder="placeholder" />
  
      <!-- Dropdown Menu -->
      <div class="dropdown-content"
        v-show="optionsShown">
        <div
          class="dropdown-item py-2"
          @mousedown="selectOption(option)"
          v-for="(option, index) in filteredOptions"
          :key="index">
            {{ option }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
    export default {
      name: 'Dropdown',
      template: 'Dropdown',
      props: {
        classe: {
          type: String,
          required: false,
          default: '',
          note: 'Border style'
        },
        valor: {
          type: String,
          required: false,
          default: '',
          note: 'Two way binding'
        },
        name: {
          type: String,
          required: false,
          default: 'dropdown',
          note: 'Input name'
        },
        options: {
          type: Array,
          required: true,
          default: () => [],
          note: 'Options of dropdown. An array of options with id and name',
        },
        placeholder: {
          type: String,
          required: false,
          default: 'Please select an option',
          note: 'Placeholder of dropdown'
        },
        disabled: {
          type: Boolean,
          required: false,
          default: false,
          note: 'Disable the dropdown'
        },
        maxItem: {
          type: Number,
          required: false,
          default: 6,
          note: 'Max items showing'
        }
      },
      data() {
        return {
          selected: {},
          optionsShown: false,
          searchFilter: ''
        }
      },
      computed: {
        filteredOptions() {
          const filtered = [];
          const regOption = new RegExp(this.searchFilter, 'ig');
          for (const option of this.options) {
            if (this.searchFilter.length < 1 || option.match(regOption)){
              if (filtered.length < this.maxItem) filtered.push(option);
            }
          }
          return filtered;
        }
      },
      methods: {
        selectOption(option) {
          this.selected = option;
          this.optionsShown = false;
          this.searchFilter = this.selected;
          this.$emit('selected', this.selected);
        },
        showOptions(){
          if (!this.disabled) {
            this.searchFilter = '';
            this.optionsShown = true;
          }
        },
        exit() {
          if (!this.selected) {
            this.selected = '';
            this.searchFilter = '';
          } else {
            this.searchFilter = this.selected;
          }
          this.$emit('selected', this.selected);
          this.optionsShown = false;
        },
        // Selecting when pressing Enter
        keyMonitor: function(event) {
          if (event.key === "Enter" && this.filteredOptions[0])
            this.selectOption(this.filteredOptions[0]);
        }
      },
      watch: {
        searchFilter() {
          if (this.filteredOptions.length === 0) {
            this.selected = {};
          } else {
            this.selected = this.filteredOptions[0];
          }
          this.$emit('filter', this.searchFilter);
        },
        valor(){
          this.searchFilter = this.valor
        }
      }
    };
  </script>
  
  
  <style lang="scss" scoped>
    .dropdown {
      position: relative;
      display: block;
      margin: auto;
      .dropdown-input { 
        cursor: pointer;  
        display: block;   
        &:hover {
          background: #f8f8fa;
        }
      }
      .dropdown-content {
        position: absolute;
        background-color: #fff;
        min-width: 248px; 
        max-height: 248px; 
        box-shadow: 0px -8px 34px 0px rgba(0,0,0,0.05);
        overflow: auto;
        z-index: 1;
        .dropdown-item { 
          line-height: 1.2em;
          padding: 8px;
          text-decoration: none;
          display: block;
          cursor: pointer;
          &:hover {
            background-color: #f8f9fa;
          }
        }
      }
      .dropdown:hover .dropdowncontent {
        display: block;
      }
    }
  </style>