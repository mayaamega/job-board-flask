'use client'

import { useEffect, useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { API_ENDPOINTS, fetchApi } from '../../api/config'

interface JobDetail {
  id: number
  title: string
  company_name: string
  location: string
  salary_range: string
  description: string
  requirements: string
  avg_rating: number
  company_description: string
}

export default function JobDetailPage({ params }: { params: { id: string } }) {
  const [job, setJob] = useState<JobDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadJob = async () => {
      try {
        const data = await fetchApi(`${API_ENDPOINTS.jobs}/${params.id}`)
        setJob(data)
      } catch (err) {
        setError('Failed to load job details')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadJob()
  }, [params.id])

  if (loading) return <p className="text-center p-6">Loading job details...</p>
  if (error) return <p className="text-center text-red-500 p-6">{error}</p>
  if (!job) return <p className="text-center p-6">Job not found</p>

  return (
    <main className="container mx-auto p-6">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-3xl">{job.title}</CardTitle>
          <CardDescription className="text-xl">{job.company_name}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-2">Location</h2>
              <p>{job.location}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">Salary Range</h2>
              <p>{job.salary_range}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">Job Description</h2>
              <p className="whitespace-pre-wrap">{job.description}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">Requirements</h2>
              <p className="whitespace-pre-wrap">{job.requirements}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">About the Company</h2>
              <p>{job.company_description}</p>
              {job.avg_rating && (
                <p className="mt-2">Company Rating: {job.avg_rating.toFixed(1)} / 5</p>
              )}
            </div>
            <Button className="w-full mt-6" size="lg">Apply Now</Button>
          </div>
        </CardContent>
      </Card>
    </main>
  )
}