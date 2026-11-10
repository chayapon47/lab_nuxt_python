import courses from '../../../public/data/courses.json'
import enrollments from '../../../public/data/enrollments.json'
export default defineEventHandler(() => ({
  count: courses.length,
  data: courses.map(course => ({
    ...course,
    enrollment_count: enrollments.filter(e => e.course_id === course.course_id).length
  }))
}))
