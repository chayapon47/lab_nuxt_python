import { z } from 'zod'
import { getDb } from '../../../utils/sqlite'
const schema=z.object({student_id:z.number().int().positive(),name:z.string().min(1),faculty:z.string().min(1),year:z.number().int().min(1).max(8),gpa:z.number().min(0).max(4),active:z.boolean(),skills:z.array(z.string())}).strict()
export default defineEventHandler(async event=>{
  const parsed=schema.safeParse(await readBody(event))
  if(!parsed.success) throw createError({statusCode:422,statusMessage:'Invalid student',data:parsed.error.flatten()})
  const s=parsed.data
  try {
    getDb().prepare('INSERT INTO students VALUES (?,?,?,?,?,?,?)').run(s.student_id,s.name,s.faculty,s.year,s.gpa,Number(s.active),JSON.stringify(s.skills))
  } catch(e:any) {
    if(String(e.code).startsWith('SQLITE_CONSTRAINT')) throw createError({statusCode:409,statusMessage:'Duplicate ID or constraint failed'})
    throw e
  }
  setResponseStatus(event,201)
  return {source:'sqlite',data:s}
})
