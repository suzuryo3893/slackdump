'''
Generate html from slackdump jsons.
(c) 2019 Ryota Suzuki. All rights reserved.
See LICENCE for details.
'''
import os,sys,re,json
from lxml import etree
import html
from datetime import datetime

def main():
    with open("users.json","r",encoding="utf8") as fp:
        users=json.load(fp)
    with open("channels.json","r",encoding="utf8") as fp:
        channels=json.load(fp)

    usersd={}
    for m in users["members"]:
        dn=m["profile"]["display_name"] if "display_name" in m["profile"] and len(m["profile"]["display_name"])>0 else m["profile"]["real_name"]
        usersd.update({m["id"]:dn})

    #sort messages by timestamp
    for ch in channels:
        ch["history"]["messages"]=sorted(ch["history"]["messages"],key=lambda m: float(m["ts"]),reverse=False)
    
    root=etree.Element("html")

    head=etree.SubElement(root,"head")
    style=etree.SubElement(head,"style")
    style.text='''
    .name{
        font-weight : bold;
    }
    .time{
        font-style : italic;
        color : #AAAAAA;
    }
    .message{
        
    }
    '''

    body=etree.SubElement(root,"body")

    #users["members"]
    for ch in channels:
        cht=etree.SubElement(body,"h1")
        cht.text="#"+ch["name"]
        ul=etree.SubElement(body,"ul")
        for msg in ch["history"]["messages"]:
            li=etree.SubElement(ul,"li")
            dts=datetime.fromtimestamp(int(msg["ts"].split(".")[0])).strftime('%Y/%m/%d %H:%M:%S')
            ttmsg=msg["text"]
            tmsg=""
            while True:
                res=re.search("<@.+?>",ttmsg)
                if not res: break
                cun=usersd[ttmsg[res.start()+2:res.end()-1]]
                tmsg+=ttmsg[:res.start()]+"<@"+cun+">"
                ttmsg=ttmsg[res.end():]
            lines=re.split("\r?\n",html.unescape(tmsg+ttmsg))

            sp=etree.SubElement(li,"span")
            sp.set("class","name")
            sp.text=usersd[msg["user"]]
            sp.tail="\t"

            sp=etree.SubElement(li,"span")
            sp.set("class","time")
            sp.text=dts

            etree.SubElement(li,"br")
            
            sp=etree.SubElement(li,"span")
            sp.set("class","message")
            sp.text=lines[0]
            for i in range(1,len(lines)):
                br=etree.SubElement(sp,"br")
                br.tail=lines[i]

            if "replies" in msg:
                msg["replies_body"]["messages"]=sorted(msg["replies_body"]["messages"],key=lambda m: float(m["ts"]))
                iul=etree.SubElement(li,"ul")
                rep_msgs=msg["replies_body"]["messages"][1:]
                for rmsg in rep_msgs:
                    ili=etree.SubElement(iul,"li")
                    dts=datetime.fromtimestamp(int(rmsg["ts"].split(".")[0])).strftime('%Y/%m/%d %H:%M:%S')
                    ttmsg=rmsg["text"]
                    tmsg=""
                    while True:
                        res=re.search("<@.+?>",ttmsg)
                        if not res: break
                        cun=usersd[ttmsg[res.start()+2:res.end()-1]]
                        tmsg+=ttmsg[:res.start()]+"<@"+cun+">"
                        ttmsg=ttmsg[res.end():]
                    lines=re.split("\r?\n",html.unescape(tmsg+ttmsg))

                    sp=etree.SubElement(ili,"span")
                    sp.set("class","name")
                    sp.text=usersd[rmsg["user"]]
                    sp.tail="\t"

                    sp=etree.SubElement(ili,"span")
                    sp.set("class","time")
                    sp.text=dts

                    etree.SubElement(ili,"br")
                    
                    sp=etree.SubElement(ili,"span")
                    sp.set("class","message")
                    sp.text=lines[0]
                    for i in range(1,len(lines)):
                        br=etree.SubElement(sp,"br")
                        br.tail=lines[i]


    with open("result.html","w",encoding="utf8") as fp:
        fp.write(etree.tostring(root,pretty_print=True,encoding="utf8").decode("utf8"))


if __name__ == "__main__":
    main()
