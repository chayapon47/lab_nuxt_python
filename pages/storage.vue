<script setup lang="ts">
const sources = [
 {name:'JSON',url:'/api/storage/json/students'},
 {name:'SQLite',url:'/api/storage/sqlite/students'},
 {name:'MongoDB',url:'/api/storage/mongo/students'}
]
const results = ref<Record<string, unknown>>({})
async function load(name:string,url:string){
 try {results.value[name]=await $fetch(url)}
 catch(e:any){results.value[name]={error:e?.data?.statusMessage||e?.message}}
}
</script>
<template>
 <main style="max-width:900px;margin:3rem auto;font-family:system-ui,sans-serif">
  <h1>Nuxt Storage Labs: JSON / SQLite / MongoDB</h1>
  <p>ทดลอง GET นักศึกษา 30 รายการจาก 3 แหล่งข้อมูล</p>
  <button v-for="s in sources" :key="s.name" style="margin:8px;padding:10px" @click="load(s.name,s.url)">Load {{s.name}}</button>
  <section v-for="s in sources" :key="s.name"><h2>{{s.name}}</h2><pre style="white-space:pre-wrap;max-height:300px;overflow:auto">{{JSON.stringify(results[s.name]||'ยังไม่ได้เรียก API',null,2)}}</pre></section>
  <NuxtLink to="/">กลับหน้าหลัก</NuxtLink>
 </main>
</template>
