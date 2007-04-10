require 'webrick'


server = WEBrick::HTTPServer.new(
  { :BindAddress => '127.0.0.1',
    :Port => '10080' })
trap('INT'){ server.shutdown }
server.mount('/', WEBrick::HTTPServlet::CGIHandler, 'ruby trpy.cgi')
server.mount('/css', WEBrick::HTTPServlet::FileHandler, './css')
server.start

