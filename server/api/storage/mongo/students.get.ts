import { getMongo } from '../../../utils/mongo'
export default defineEventHandler(async event=>{
  const q=getQuery(event)
  const faculty=typeof q.faculty==='string'?q.faculty:undefined
  try {
    const collection=(await getMongo(event)).collection('students')
    const filter=faculty?{faculty}:{}
    const data=await collection.find(filter,{projection:{_id:0}}).sort({student_id:1}).limit(100).toArray()
    return {source:'mongodb',count:data.length,data}
  } catch { throw createError({statusCode:503,statusMessage:'MongoDB unavailable; start Docker and seed first'}) }
})
