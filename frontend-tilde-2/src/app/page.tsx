import Link from "next/link"


export default function Home() {
  return (
    <main>

      <Link href="/login">login</Link>
      <Link href="/forgot-password">forgot password</Link>
      <Link href="/user/board">user board</Link>

    </main>
  )
}
