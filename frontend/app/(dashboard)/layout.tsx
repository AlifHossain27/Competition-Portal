import DesktopSidebar, { MobileSidebar } from "@/components/Sidebar"
import { Separator } from "@/components/ui/separator"
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen">
      <DesktopSidebar />
      <div className="flex flex-col flex-1 min-h-screen">
      <header className="flex items-center px-2 py-4 h-[55px] container">
        <MobileSidebar/>
        <Link href="/">
          <span className="text-xl font-bold font-headline text-foreground">Competition Portal</span>
        </Link>
      </header>
      <Separator/>
      <div className="overflow-auto">
        <div className="flex-1 container text-accent-foreground">
          {children}
        </div>
      </div>
      </div>
    </div>
  )
}
