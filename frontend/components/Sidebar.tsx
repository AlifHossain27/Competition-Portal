"use client"
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from 'next/navigation'
import { CalendarClock, ChartColumnBig, LogOut, MenuIcon, Network, Settings, Users } from 'lucide-react'
import { usePathname } from 'next/navigation'
import { useDispatch } from 'react-redux'
import { AppDispatch, useAppSelector } from '@/redux/store'
import { logIn, logOut } from '@/redux/features/auth-slice'
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from './ui/sheet'
import { Button } from './ui/button'
import { toast } from "sonner"
import { uppercase } from "zod";

const regularRoutes = [
    {href: "/dashboard", label: "Dashboard", icon: ChartColumnBig},
    {href: "/settings", label: "Settings", icon: Settings}
]

const adminRoutes = [
    {href: "/dashboard", label: "Dashboard", icon: ChartColumnBig},
    {href: "/users", label: "Users", icon: Users},
    {href: "/clubs", label: "Clubs", icon: Network},
    {href: "/settings", label: "Settings", icon: Settings}
]

const clubRoutes = [
    {href: "/dashboard", label: "Dashboard", icon: ChartColumnBig},
    {href: "/club", label: "Club", icon: Network},
    {href: "/events", label: "Events", icon: CalendarClock},
    {href: "/settings", label: "Settings", icon: Settings}
]

export function useUserInfo() {
  const [clubName, setClubName] = useState("");
  const dispatch = useDispatch<AppDispatch>();
  const router = useRouter();
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    (async () => {
      try {
        const resp = await fetch(`${API_BASE_URL}/api/user/me/`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
        });
        const data = await resp.json();

        setClubName(data.club?.name ?? data.role.toUpperCase());

        if (resp.ok) {
          dispatch(logIn(data.role));
        } else {
          dispatch(logOut());
          router.push("/");
        }
      } catch {
        console.log("connection failed");
      }
    })();
  }, [dispatch, API_BASE_URL, router]);

  return clubName;
}

export function LogoutButton() {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
  const router = useRouter();
  const dispatch = useDispatch<AppDispatch>();

  const handleLogout = async () => {
    await fetch(`${API_BASE_URL}/api/auth/logout/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    });

    toast("Logged out");
    dispatch(logOut());
    router.push("/");
  };

  return (
    <Button
      variant="ghost"
      className="flex w-full justify-start gap-2 p-4 items-center rounded-md h-14 text-md text-muted-foreground hover:bg-red-600 hover:text-white"
      onClick={handleLogout}
    >
      <span/>
      <LogOut size={20} />
      Logout
    </Button>
  );
}


export default function DesktopSidebar() {
  const clubName = useUserInfo();
  const userType = useAppSelector((state) => state.auth.value.userType)
  const pathname = usePathname();

  let routes = regularRoutes
  if (userType === "admin") {
    routes = adminRoutes;
  } else if (userType === "club") {
    routes = clubRoutes;
  }

  return (
    <div className='hidden relative md:block min-w-[280px] max-w-[280px] h-screen overflow-hidden w-full bg-primary/5 text-muted-foreground border-r-2 border-separate'>
        <div className='flex items-center justify-center gap-2 border-b-[1px] border-separate p-4'>
            <span>{clubName}</span>
        </div>
        <div className='flex flex-col p-2 gap-2'>
          {routes.map((route) => {
          const isActive = pathname === route.href;

          return (
            <Link
              key={route.href}
              href={route.href}
              className={`
                flex gap-2 p-4 items-center
                rounded-md
                ${isActive 
                  ? 'bg-primary text-white font-semibold'
                  : 'hover:bg-primary/20 text-muted-foreground'}
              `}
            >
              <route.icon size={20} />
              {route.label}
            </Link>
          )
        })}
        </div>
       <div className="flex flex-col px-2 gap-2">
          <LogoutButton />
        </div>

    </div>
  )
}

export function MobileSidebar() {
  const [isOpen, setOpen] = useState(false)
  const clubName = useUserInfo();
  const userType = useAppSelector((state) => state.auth.value.userType)
  const pathname = usePathname();
  let routes = regularRoutes
  if (userType === "admin") {
    routes = adminRoutes;
  } else if (userType === "club") {
    routes = clubRoutes;
  }
  return (
    <div className='block border-separate bg-background md:hidden'>
      <nav className='container flex items-center justify-between px-8'>
        <Sheet open={isOpen} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <MenuIcon/>
            </Button>
          </SheetTrigger>
          <SheetContent  side='left'>
            <SheetTitle>
              <div className='flex items-center justify-center gap-2 border-b-[1px] border-separate p-4 font-medium'>
                  <span>{clubName}</span>
              </div>
            </SheetTitle>
            <div className='flex flex-col px-2 gap-2'>
              {routes.map((route) => {
              const isActive = pathname === route.href;

              return (
                <Link
                  key={route.href}
                  href={route.href}
                  className={`
                    flex gap-2 p-4 items-center
                    rounded-md
                    ${isActive 
                      ? 'bg-primary text-white font-semibold'
                      : 'hover:bg-primary/20 text-muted-foreground'}
                  `}
                  onClick={() => setOpen((prev) => !prev)}
                >
                  <route.icon size={20} />
                  {route.label}
                </Link>
              )
            })}
            </div>
            <div className="flex flex-col px-2 gap-2">
              <LogoutButton />
            </div>
          </SheetContent>
        </Sheet>
      </nav>
    </div>
  )
}

