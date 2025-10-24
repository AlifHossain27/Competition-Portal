"use client";

import React from "react";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
 // adjust path if needed

// HoverUnderline Function

interface HoverUnderlineProps {
  text: string;
}

const HoverUnderline: React.FC<HoverUnderlineProps> = ({ text }) => {
  return (
    <p className="relative inline-block text-lg font-medium group cursor-pointer">
      <span className="text-foreground/80 hover:text-foreground transition-colors duration-300 ">
        {text}
      </span>
      <span
        className="absolute left-0 bottom-[-3] h-[2px] w-0 bg-black transition-all duration-300 group-hover:w-full "
      ></span>
    </p>
  );
};


export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  // Detect scroll
  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/events", label: "Events" },
    { href: "/clubs", label: "Clubs" },
  ];

  const navbarActive = isScrolled || isOpen; // blur if scrolled or menu open

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        navbarActive ? "backdrop-blur-sm shadow-sm" : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <button className="text-xl font-bold text-black select-none">
            Competation Portal
          </button>

          {/* Desktop Links */}
          <div className="hidden md:flex space-x-8 text-black font-medium">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="group">
                <HoverUnderline text={link.label} />
              </Link>
            ))}
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
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className="block group text-center"
              >
                <HoverUnderline text={link.label} />
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}
