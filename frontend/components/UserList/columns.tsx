"use client"
import { ColumnDef } from "@tanstack/react-table"


export type Users = {
    uuid: string
    name: string
    email: string
    university_id: string
    role: string
}

export const columns: ColumnDef<Users>[] = [
    {
      accessorKey: "name",
      header: "Name",
    },
    
    {
      accessorKey: "email",
      header: "Email",
    },
    {
      accessorKey: "university_id",
      header: "University ID",
    },
    {
      accessorKey: "role",
      header: "User Type",
    },
    {
      id: "actions",
      header: "Actions",
      cell: ({ row }) => {
        const data = row.original
        return (
          <div className="flex gap-2">
            <h1>Update</h1>
            <h1>Delete</h1>
          </div>
        )
      },
    },
  ]