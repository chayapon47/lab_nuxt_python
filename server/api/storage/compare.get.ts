import students from '../../data/students.json'
import { getDb } from '../../utils/sqlite'
export default defineEventHandler(()=>{
  const sqliteCount=(getDb().prepare('SELECT COUNT(*) AS n FROM students').get() as {n:number}).n
  return {json:students.length,sqlite:sqliteCount,
    note:'MongoDB is optional and can be compared using /api/storage/mongo/students'}
})
