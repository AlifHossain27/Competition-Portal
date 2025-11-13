"use client";

import React from "react";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button';
import { Menu, X } from "lucide-react";
import { toast } from "sonner"
import { useDispatch } from 'react-redux'
import { AppDispatch, useAppSelector } from '@/redux/store'
import { logIn, logOut } from '@/redux/features/auth-slice'




export default function Header() {
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
  const router = useRouter()
  const dispatch = useDispatch<AppDispatch>()
  const isAuth = useAppSelector((state) => state.auth.value.isAuthenticated)

  const [isScrolled, setIsScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Detect scroll
  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const logout = async () => {
    await fetch(`${API_BASE_URL}/api/auth/logout/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
    })
    toast("Logged out")
    dispatch(logOut())
    router.push('/')
  }

  useEffect(() => {
    (async () => {
      try {
        const resp = await fetch(`${API_BASE_URL}/api/user/me/`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
        })
        const data = await resp.json();
        console.log(data)
        if (resp.ok) {
          dispatch(logIn(data.role))
        } else {
          dispatch(logOut())
        }
      } catch {
        console.log('connection failed')
      }
    })()
  }, [dispatch, API_BASE_URL])

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events" },
    { href: "/clubs", label: "Clubs" },
  ];

  const adminNavLinks = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events" },
    { href: "/clubs", label: "Clubs" },
    { href: "/dashboard", label: "Dashboard" },
  ];

  const regularNavLinks = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events" },
    { href: "/clubs", label: "Clubs" },
    { href: "/dashboard", label: "Dashboard" },
  ];

  const clubNavLinks = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events" },
    { href: "/clubs", label: "Clubs" },
    { href: "/dashboard", label: "Dashboard" },
  ];

  const navbarActive = isScrolled || isOpen;
  const linksToShow = isAuth ? adminNavLinks : navLinks;

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        navbarActive ? "backdrop-blur-sm shadow-sm" : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2" >
            <span className="text-xl font-bold font-headline text-foreground">Competition Portal</span>
          </Link>

          {/* Desktop Links */}
          <div className="hidden md:flex ml-4 space-x-4">
            {linksToShow.map((link) => (
              <Link 
                key={link.href} 
                href={link.href}
                className='text-foreground/80 hover:text-foreground text-sm font-medium p-2 relative group cursor-pointer'
              >
                {link.label}
                <span className='absolute bottom-[-3px] left-0 w-full h-[2px] bg-black scale-x-0 group-hover:scale-x-100 origin-left transition-transform duration-300 ease-in-out z-10'></span>
              </Link>
            ))}
            {isAuth && (
              <Button variant="destructive" className="text-sm" onClick={logout}>
                Logout
              </Button>
            )}
          </div>

          

          {/* Mobile Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden text-black"
            aria-label="Toggle Menu"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden backdrop-blur-sm  shadow-md ">
          <div className="px-4 py-6 flex flex-col items-center space-y-4 text-black font-medium">
            {linksToShow.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className="block group text-center"
              >
                {link.label}
              </Link>
            ))}
            {isAuth && (
              <Button variant="destructive" className="text-sm" onClick={logout}>
                Logout
              </Button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
