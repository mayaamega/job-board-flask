'use client'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function HomePage() {
  return (
    <main className="container mx-auto p-6">
      <h1 className="text-4xl font-bold mb-6">Welcome to Job Board</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Find Jobs</CardTitle>
            <CardDescription>Browse through thousands of job listings</CardDescription>
          </CardHeader>
          <CardContent>
            <Button className="w-full">Search Jobs</Button>
          </CardContent>
        </Card>
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