import Hero from "@/components/Hero";
import Image from "next/image";

export default function Home() {
  return (
    <div className="flex flex-col bg-background">
      
      <main className="flex-grow">
        <Hero/>
      </main>
      
    </div>
  );
}
