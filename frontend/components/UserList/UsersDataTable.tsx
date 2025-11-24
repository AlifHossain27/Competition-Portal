import React from 'react'
import {  Users, columns } from "./columns"
import { DataTable } from "./dataTable"
import { cookies } from "next/headers"

async function getData(): Promise<Users[]> {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
    const cookieStore = await cookies();
    const cookieHeader = cookieStore
    .getAll()
    .map((c) => `${c.name}=${c.value}`)
    .join("; ");
    const resp = await fetch(`${API_BASE_URL}/api/users/`,{
        method: "GET",
        headers: { Cookie: cookieHeader, },
        credentials: 'include',
      
    });
    const data = await resp.json()
    return data
}

export default async function UsersDataTable() {
    const data = await getData()
    return (
      <div className='w-auto col-span-2 overflow-auto relative'>
        <DataTable columns={columns} data={data} />
      </div>
    )
  }