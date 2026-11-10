import students from '../../public/data/students.json'
export type Student = { student_id: number; name: string; faculty: string; year: number; gpa: number; active: boolean; skills: string[] }
export const studentStore = new Map<number, Student>(
  (students as Student[]).map(s => [s.student_id, structuredClone(s)])
)
// Training only: changes disappear when the server restarts.
