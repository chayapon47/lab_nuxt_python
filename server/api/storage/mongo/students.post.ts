import { z } from 'zod'
import { getMongo } from '../../../utils/mongo'
const schema=z.object({student_id:z.number().int().positive(),name:z.string().min(1),faculty:z.string().min(1),year:z.number().int().min(1).max(8),gpa:z.number().min(0).max(4),active:z.boolean(),skills:z.array(z.string())}).strict()
export default defineEventHandler(async event=>{
  const parsed=schema.safeParse(await readBody(event))
  if(!parsed.success) throw createError({statusCode:422,statusMessage:'Invalid student'})
  try {
    await (await getMongo(event)).collection('students').insertOne(parsed.data)
    setResponseStatus(event,201)
    return {source:'mongodb',data:parsed.data}
  } catch(e:any) {
    if(e?.code===11000) throw createError({statusCode:409,statusMessage:'Duplicate student_id'})
    throw createError({statusCode:503,statusMessage:'MongoDB insert failed'})
  }
})
