"use client";
import React, { useEffect } from "react";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { toast } from "sonner"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { useRouter } from 'next/navigation'

const profileFormSchema = z.object({
    username: z.string().min(2, { message: "Name must be at least 2 characters." }),
    email: z.email({ message: "Please enter a valid email address." }),
    universityId: z.string().min(8, { message: "University ID must be at least 8 characters." }),
});

const passwordFormSchema = z.object({
    currentPassword: z.string().min(8, { message: "Password must be at least 8 characters." }),
    newPassword: z.string().min(8, { message: "New password must be at least 8 characters." }),
    confirmPassword: z.string().min(8, { message: "Confirm password must be at least 8 characters." }),
}).refine((data) => data.newPassword === data.confirmPassword, {
    message: "New passwords do not match.",
    path: ["confirmPassword"],
});

export default function SettingsPage() {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;
    const router = useRouter()
    useEffect(() => {
        async function fetchProfile() {
        try {
            const res = await fetch(`${API_BASE_URL}/api/user/me`, {
            credentials: "include",
            });
            if (res.ok) {
            const user = await res.json();
            console.log(user)
            profileForm.reset({
                username: user.name,
                email: user.email,
                universityId: user.university_id
            });
            } else {
            throw new Error("Failed to fetch user data");
            }
        } catch (err) {
            console.error(err);
            toast.error("Failed to load profile data");
        }
        }

        fetchProfile();
    }, []);

    const profileForm = useForm<z.infer<typeof profileFormSchema>>({
        resolver: zodResolver(profileFormSchema),
        defaultValues: {
            username: "",
            email: "",
            universityId: "",
        },
    });

    const passwordForm = useForm<z.infer<typeof passwordFormSchema>>({
        resolver: zodResolver(passwordFormSchema),
        defaultValues: {
            currentPassword: "",
            newPassword: "",
            confirmPassword: "",
        },
    });

    async function onProfileSubmit(values: z.infer<typeof profileFormSchema>) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/user/me/`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: values.username,
                email: values.email,
                university_id: values.universityId
            }),
            });

            if (res.ok) {
                const updatedUser = await res.json();
                toast.success("Profile updated successfully");
                await router.refresh()
                profileForm.reset({
                    username: updatedUser.name,
                    email: updatedUser.email,
                    universityId: updatedUser.university_id
                });
            } else {
                const errorData = await res.json();
                console.log(errorData)
                toast.error(errorData.detail || "Failed to update profile");
            }
        } catch (err) {
            toast.error("Network error updating profile");
            console.error(err);
        }
    }

    async function onPasswordSubmit(values: z.infer<typeof passwordFormSchema>) {
        try {
            const res = await fetch(`${API_BASE_URL}/api/user/change-password`, {
            method: "PATCH",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                current_password: values.currentPassword,
                new_password: values.newPassword,
                new_password_confirm: values.confirmPassword,
            }),
            });

            if (res.ok) {
            toast.success("Password changed successfully");
            await router.refresh()
            passwordForm.reset()
            } else {
            const errorData = await res.json();
            toast.error(errorData.detail || "Failed to change password");
            }
        } catch (err) {
            toast.error("Network error changing password");
            console.error(err);
        }
        passwordForm.resetField
    }

    return (
        <div className="h-auto container mx-auto p-4 flex flex-col gap-5">
            <Card>
                <CardHeader>
                    <CardTitle>Profile Information</CardTitle>
                    <CardDescription>Update your personal details here.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...profileForm}>
                        <form onSubmit={profileForm.handleSubmit(onProfileSubmit)} className="space-y-6">
                            <FormField
                                control={profileForm.control}
                                name="username"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Username</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Your Username" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={profileForm.control}
                                name="email"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Email Address</FormLabel>
                                        <FormControl>
                                            <Input type="email" placeholder="your.email@university.edu" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={profileForm.control}
                                name="universityId"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>University ID</FormLabel>
                                        <FormControl>
                                            <Input placeholder="Your University ID" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <Button type="submit">Save Changes</Button>
                        </form>
                    </Form>
                </CardContent>
            </Card>

            <Separator />

            <Card>
                <CardHeader>
                    <CardTitle>Change Password</CardTitle>
                    <CardDescription>Update your login password. Use a strong, unique password for security.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...passwordForm}>
                        <form onSubmit={passwordForm.handleSubmit(onPasswordSubmit)} className="space-y-6">
                            <FormField
                                control={passwordForm.control}
                                name="currentPassword"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Current Password</FormLabel>
                                        <FormControl>
                                            <Input type="password" placeholder="********" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={passwordForm.control}
                                name="newPassword"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>New Password</FormLabel>
                                        <FormControl>
                                            <Input type="password" placeholder="********" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                             <FormField
                                control={passwordForm.control}
                                name="confirmPassword"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Confirm New Password</FormLabel>
                                        <FormControl>
                                            <Input type="password" placeholder="********" {...field} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <Button type="submit">Update Password</Button>
                        </form>
                    </Form>
                </CardContent>
            </Card>
        </div>
    );
}