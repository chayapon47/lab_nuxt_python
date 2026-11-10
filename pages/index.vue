<script setup lang="ts">
const labs = [
  ['01','GET JSON','อ่าน Students JSON จาก Public Dataset'],
  ['02','POST','สร้าง Student ผ่าน Nuxt Server API'],
  ['03','Errors','ตรวจ 404 และ Validation'],
  ['04','REST Provider','สร้าง GET endpoint ด้วย Nitro'],
  ['05','CRUD','POST PUT DELETE และ HTTP Status'],
  ['06','Relational Data','Courses + Enrollments'],
  ['07','Graph Model','Page / Post / Field / Edge'],
  ['08','Meta Graph API','Server-side Meta connector (optional)'],
  ['09','Pagination','แบ่งหน้ารายการ Social Posts'],
  ['10','OpenAI API','สรุปข้อความด้วย Responses API'],
  ['11','Structured JSON','Structured Outputs ด้วย Zod'],
  ['12','Integration','Course dataset → AI → JSON']
]
const selected = ref(1)
const output = ref<any>(null)
const loading = ref(false)
const input = ref('REST API เป็นรูปแบบการออกแบบ API ที่จัดการ resource ผ่าน HTTP')
const newId = ref(2001)
async function run() {
  loading.value = true; output.value = null
  try {
    let url = ''; let opts: any = {}
    switch (selected.value) {
      case 1: url='/data/students.json'; break
      case 2: url='/api/students';opts={method:'POST',body:{student_id:newId.value++,name:'Intern Student',faculty:'IT',year:2,gpa:3.2,active:true,skills:['Nuxt','API']}};break
      case 3: url='/api/students/999999';break
      case 4: url='/api/students';break
      case 5: url='/api/students/1001';break
      case 6: url='/api/courses';break
      case 7: url='/data/social_pages.json';break
      case 8: url='/api/graph/meta';break
      case 9: url='/api/graph/posts?page=1&limit=5';break
      case 10: url='/api/ai/summary';opts={method:'POST',body:{text:input.value}};break
      case 11: url='/api/ai/structured';opts={method:'POST',body:{description:input.value}};break
      case 12: url='/api/ai/course/CS101';opts={method:'POST'};break
    }
    output.value = await $fetch(url,opts)
  } catch (e:any) {
    output.value = {error:true,status:e?.statusCode||e?.status||'unknown',message:e?.data?.statusMessage||e?.message}
  } finally { loading.value=false }
}
</script>
<template>
  <main class="layout">
    <h1>Nuxt API Intern Training — 12 Labs</h1>
    <p>ข้อมูลจำลองชุดเดียวกับ Python Labs (149 records) · เรียก OpenAI เฉพาะเมื่อผู้เรียนกด Run</p>
    <section class="grid">
      <button v-for="lab in labs" :key="lab[0]" :class="{active:selected===Number(lab[0])}" @click="selected=Number(lab[0]);output=null">
        <strong>{{lab[0]}} — {{lab[1]}}</strong><small>{{lab[2]}}</small>
      </button>
    </section>
    <section class="panel">
      <h2>Lab {{selected}}: {{labs[selected-1]?.[1]}}</h2>
      <p>{{labs[selected-1]?.[2]}}</p>
      <label v-if="[10,11].includes(selected)">Input <textarea v-model="input" maxlength="2000" rows="3" /></label>
      <button class="run" :disabled="loading" @click="run">{{loading?'Loading...':'Run example'}}</button>
      <p v-if="[8,10,11,12].includes(selected)" class="warn">ต้องตั้งค่า Secret ฝั่ง Server; OpenAI อาจมีค่าใช้จ่าย และควรใช้เฉพาะ localhost</p>
      <pre>{{output===null?'กด Run เพื่อดูผลลัพธ์':JSON.stringify(output,null,2)}}</pre>
    </section>
  </main>
</template>
<style>
body{font-family:system-ui,'Noto Sans Thai',sans-serif;background:#f6f8fb;color:#1c2635}
.layout{max-width:1050px;margin:35px auto;padding:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}
button{cursor:pointer;text-align:left;border:1px solid #cbd5e1;background:white;border-radius:9px;padding:13px;color:#1c2635}
button.active{border-color:#2563eb;background:#eff6ff}
small{display:block;margin-top:5px;color:#475569}
.panel{background:white;padding:20px;margin-top:24px;border-radius:12px;border:1px solid #dce2ea}
.run{background:#1d4ed8;color:white;margin:12px 0}
textarea{display:block;width:100%;box-sizing:border-box}
pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0f172a;color:#dbeafe;padding:15px;border-radius:8px;max-height:500px;overflow:auto}
.warn{color:#9a3412}
</style>
