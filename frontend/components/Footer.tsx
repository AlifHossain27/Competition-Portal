import Link from 'next/link';
import { Bot, Twitter, Rss, Github } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

const Footer = () => {
    return (
        <footer className="bg-card border-t border-border">
            <div className="container mx-auto py-12 px-4 md:px-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                    <div className="space-y-4 md:col-span-1">
                        <Link href="/" className="flex items-center gap-2">
                            <Bot className="h-8 w-8 text-primary" />
                            <span className="text-2xl font-bold font-headline text-foreground">SyncUp</span>
                        </Link>
                        <p className="text-muted-foreground text-sm">The newsletter of the University Computer Club.</p>
                    </div>
                    <div className="md:col-span-2 grid grid-cols-2 sm:grid-cols-3 gap-8">
                        <div>
                            <h4 className="font-semibold mb-4 text-foreground">Quick Links</h4>
                            <ul className="space-y-2">
                                <li><Link href="#content" className="text-sm text-muted-foreground hover:text-black transition-colors">Articles</Link></li>
                                <li><Link href="#authors" className="text-sm text-muted-foreground hover:text-black transition-colors">Authors</Link></li>
                                <li><Link href="#contact" className="text-sm text-muted-foreground hover:text-black transition-colors">Contact</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4 text-foreground">Community</h4>
                            <ul className="space-y-2">
                                <li><Link href="#" className="text-sm text-muted-foreground hover:text-black transition-colors">About The Club</Link></li>
                                <li><Link href="/events" className="text-sm text-muted-foreground hover:text-black transition-colors">Events</Link></li>
                                <li><Link href="#" className="text-sm text-muted-foreground hover:text-black transition-colors">Join Us</Link></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4 text-foreground">Follow Us</h4>
                            <div className="flex gap-4">
                                <Link href="#" aria-label="Twitter">
                                    <Twitter className="h-5 w-5 text-muted-foreground hover:text-black transition-colors" />
                                </Link>
                                 <Link href="#" aria-label="GitHub">
                                    <Github className="h-5 w-5 text-muted-foreground hover:text-black transition-colors" />
                                </Link>
                                <Link href="#" aria-label="RSS Feed">
                                    <Rss className="h-5 w-5 text-muted-foreground hover:text-black transition-colors" />
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
                <Separator className="my-8 bg-border/50" />
                <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-muted-foreground">
                    <p>© {new Date().getFullYear()} University Computer Club. All rights reserved.</p>
                    <p>Made with 💙 by club members.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;