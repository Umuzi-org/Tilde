import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { Button } from "@/components/ui/button"

function AgileCard(){
    return <Card style={{borderLeft: "10px solid green"}} className="w-[350px]">
    <CardHeader>
      <CardTitle>Card Title</CardTitle>
      <CardDescription>Card Description</CardDescription>
    </CardHeader>
    <CardContent>
      Assignee 
      Reviewers 
    </CardContent>
    <CardFooter>
      <Button>Start</Button>
      <Button>Details</Button>
      <Button>Content</Button>
    </CardFooter>
  </Card>
}

function Column({children, heading}: {children: React.ReactNode, heading: string}){
    return (
    <div className="border-solid border-2">
        <h2 className="centre">{heading}</h2>
        <ScrollArea className="rounded-md">
        {children}
        </ScrollArea>
    </div>)
}


export default function Board() {
    return (
  
  <div class="grid grid-cols-5 gap-4">
  

        <Column heading="Backlog">
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        </Column>

        <Column heading="In Progress">
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        <AgileCard/>
        </Column>

        <Column heading="Feedback"></Column>
        <Column heading="Review"></Column>
        <Column heading="Done!"></Column>


</div>
  
    )
  }
  