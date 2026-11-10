import { getDb } from '../../../utils/sqlite'
export default defineEventHandler(event => {
  const q = getQuery(event)
  const id = Number(q.student_id)
  if (!Number.isInteger(id) || id <= 0) throw createError({statusCode:400,statusMessage:'student_id required'})
  const data = getDb().prepare(`
    SELECT e.enrollment_id,s.student_id,s.name,c.course_id,c.course_name,e.score
    FROM enrollments e JOIN students s ON e.student_id=s.student_id
    JOIN courses c ON e.course_id=c.course_id
    WHERE s.student_id=? ORDER BY c.course_id`).all(id)
  return {source:'sqlite',count:data.length,data}
})
