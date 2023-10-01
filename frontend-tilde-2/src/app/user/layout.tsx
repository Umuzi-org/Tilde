
export default function UserLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div>

    <nav className="">

        Board 
        Activity 
        Performance    
        Profile 
    </nav>
    <main>
        {children}
    </main>
    </div>
  )
}
