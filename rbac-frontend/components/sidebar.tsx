"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { LogOut, User, Building, Shield } from "lucide-react"
import { toast } from "sonner"

export default function Sidebar() {
    const router = useRouter()
    const [username, setUsername] = useState<string | null>(null)
    const [role, setRole] = useState<string | null>(null)

    useEffect(() => {
        setUsername(localStorage.getItem("username"))
        setRole(localStorage.getItem("user_role"))
    }, [])

    const handleLogout = () => {
        localStorage.removeItem("access_token")
        localStorage.removeItem("username")
        localStorage.removeItem("user_role")
        toast.success("Logged out")
        router.push("/login")
    }

    const getVisibleDepts = () => {
        const allDepts = ["Finance", "HR", "Marketing", "Engineering", "General"]
        if (!role) return ["General"]

        const userRole = role.toLowerCase()
        if (userRole === "c-level") return allDepts

        // Match role name to department name
        const roleToDept: Record<string, string> = {
            "finance": "Finance",
            "hr": "HR",
            "marketing": "Marketing",
            "engineering": "Engineering"
        }

        const specificDept = roleToDept[userRole]
        return specificDept ? [specificDept, "General"] : ["General"]
    }

    return (
        <div className="w-64 border-r border-white/10 bg-black/60 backdrop-blur-xl flex flex-col h-full">
            <div className="p-6 border-b border-white/10 flex items-center gap-2">
                <Shield className="w-8 h-8 text-blue-500" />
                <span className="font-bold text-xl bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    RBAC AI
                </span>
            </div>

            <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        Departments
                    </div>
                    {getVisibleDepts().map((deptName) => (
                        <Button
                            key={deptName}
                            variant="ghost"
                            className="w-full justify-start text-gray-400 hover:text-white hover:bg-white/5"
                            onClick={() => router.push(`/dashboard?dept=${deptName.toLowerCase()}`)}
                        >
                            <Building className="mr-2 h-4 w-4" />
                            {deptName}
                        </Button>
                    ))}
                </div>
            </ScrollArea>

            <div className="p-4 border-t border-white/10 space-y-4">
                <div className="flex items-center gap-3">
                    <Avatar>
                        <AvatarImage src="" />
                        <AvatarFallback className="bg-blue-600">
                            {username ? username[0].toUpperCase() : "U"}
                        </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-white truncate">
                            {username || "User"}
                        </p>
                        <p className="text-xs text-gray-500 truncate">Online</p>
                    </div>
                </div>
                <Button variant="destructive" className="w-full justify-start" onClick={handleLogout}>
                    <LogOut className="mr-2 h-4 w-4" />
                    Log Out
                </Button>
            </div>
        </div>
    )
}
