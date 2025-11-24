import UsersDataTable from '@/components/UserList/UsersDataTable'
import React from 'react'

const UsersPage = () => {
  return (
    <div className="flex flex-col bg-background">
      
      <main className="container mx-auto p-4 flex flex-col gap-6">
        <UsersDataTable/>
      </main>
      
    </div>
  )
}

export default UsersPage