'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { API_ENDPOINTS, fetchApi } from './api/config'
   
interface Job {
  id: number
  title: string
  company_name: string
  location: string
  salary_range: string
  avg_rating: number
}
  export default function HomePage() {
  const router = useRouter()
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadJobs = async () => {
      try {
        const data = await fetchApi(API_ENDPOINTS.jobs)
        setJobs(data)
      } catch (err) {
        setError('Failed to load jobs')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadJobs()
  }, [])

  const handleViewJob = (jobId: number) => {
    router.push(`/job/${jobId}`)
  }
   
  return (
    <main className="container mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6">Welcome to Job Board</h1>
      
      {loading ? (
        <p className="text-center">Loading jobs...</p>
      ) : error ? (
        <p className="text-center text-red-500">{error}</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {jobs.map(job => (
            <Card key={job.id}>
              <CardHeader>
                <CardTitle>{job.title}</CardTitle>
                <CardDescription>{job.company_name}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="mb-2">{job.location}</p>
                <p className="mb-4">{job.salary_range}</p>
                <Button className="w-full" onClick={() => handleViewJob(job.id)}>View Details</Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mt-8">
        <Card>
          <CardHeader>
            <CardTitle>Post a Job</CardTitle>
            <CardDescription>Reach thousands of potential candidates</CardDescription>
          </CardHeader>
          <CardContent>
            <Button className="w-full" variant="outline">Post Now</Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Create Account</CardTitle>
            <CardDescription>Access personalized job recommendations</CardDescription>
          </CardHeader>
          <CardContent>
            <Button className="w-full" variant="secondary">Sign Up</Button>
          </CardContent>
        </Card>
      </div>
    </main>
  )
}