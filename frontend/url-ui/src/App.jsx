import { useState, useEffect } from "react"

function App() {

  const backend = "http://127.0.0.1:5000"

  const [url,setUrl] = useState("")
  const [custom,setCustom] = useState("")
  const [expires,setExpires] = useState("")
  const [shortUrl,setShortUrl] = useState("")
  const [analytics,setAnalytics] = useState([])


  const shorten = async()=>{

    const res = await fetch(`${backend}/shorten`,{

      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({
        url,
        custom,
        expires
      })

    })

    const data = await res.json()

    setShortUrl(data.short_url)

    fetchAnalytics()
  }


  const fetchAnalytics = async()=>{

    const res = await fetch(`${backend}/analytics`)
    const data = await res.json()

    setAnalytics(data)

  }


  const copy = ()=>{

    navigator.clipboard.writeText(shortUrl)
    alert("Copied!")

  }


  useEffect(()=>{

    fetchAnalytics()

  },[])


  return (

    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-purple-600 to-indigo-700 p-6">


      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-md">

        <h1 className="text-3xl font-bold text-center mb-6">
          🔗 URL Shortener
        </h1>


        <input
        placeholder="Enter URL"
        value={url}
        onChange={(e)=>setUrl(e.target.value)}
        className="w-full border p-3 rounded mb-3"
        />


        <input
        placeholder="Custom short code"
        value={custom}
        onChange={(e)=>setCustom(e.target.value)}
        className="w-full border p-3 rounded mb-3"
        />


        <input
        type="datetime-local"
        value={expires}
        onChange={(e)=>setExpires(e.target.value)}
        className="w-full border p-3 rounded mb-3"
        />


        <button
        onClick={shorten}
        className="w-full bg-purple-600 text-white p-3 rounded"
        >
        Shorten URL
        </button>


        {shortUrl && (

          <div className="mt-6 text-center">

            <p className="mb-2">Short URL</p>

            <a
            href={shortUrl}
            target="_blank"
            className="text-blue-600 break-all"
            >
            {shortUrl}
            </a>

            <button
            onClick={copy}
            className="mt-3 bg-green-500 text-white p-2 rounded w-full"
            >
            Copy
            </button>

            <img
            src={`${backend}/qr/${shortUrl.split("/").pop()}`}
            className="mx-auto mt-4"
            />

          </div>

        )}

      </div>


      <div className="bg-white mt-6 p-6 rounded-xl shadow-xl w-full max-w-3xl">

        <h2 className="text-xl font-bold mb-4 text-center">
          📊 Analytics
        </h2>

        <table className="w-full">

          <thead>

            <tr className="border-b">
              <th>Short</th>
              <th>Original</th>
              <th>Clicks</th>
              <th>Country</th>
              <th>City</th>
            </tr>

          </thead>


          <tbody>

            {analytics.map((a,i)=>(
              <tr key={i} className="border-b">

                <td>{a[0]}</td>
                <td className="break-all">{a[1]}</td>
                <td>{a[2]}</td>
                <td>{a[3]}</td>
                <td>{a[4]}</td>

              </tr>
            ))}

          </tbody>

        </table>

      </div>

    </div>

  )
}

export default App