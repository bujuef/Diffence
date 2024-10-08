from purchase_models import *

def train(train_loader,model,criterion,optimizer,epoch,use_cuda,device=torch.device('cuda'),num_batchs=999999,debug_='MEDIUM',batch_size=32, uniform_reg=False):
    # switch to train mode
    model.train()

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()
    
    
    end = time.time()

    for ind, (inputs,targets) in enumerate(train_loader):

        # measure data loading time
        data_time.update(time.time() - end)

        if use_cuda:
            inputs, targets = inputs.to(device), targets.to(device)
        inputs, targets = torch.autograd.Variable(inputs), torch.autograd.Variable(targets)

        # compute output
        try:
            outputs,_,_ = model(inputs)
        except:
            try:
                outputs,_ = model(inputs)
            except:
                outputs = model(inputs)
        uniform_=torch.ones(len(outputs))/len(outputs)
        
        if uniform_reg==True:
            loss = criterion(outputs, targets) + F.kl_div(uniform_,outputs)
        else:
            loss = criterion(outputs, targets)

        # measure accuracy and record loss
        prec1, prec5 = accuracy(outputs.data, targets.data, topk=(1, 5))
        losses.update(loss.item(), inputs.size(0))
        top1.update(prec1.item(), inputs.size(0))
        top5.update(prec5.item(), inputs.size(0))

        # compute gradient and do SGD step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        # plot progress
        if False and debug_=='HIGH' and ind%100==0:
            print  ('Classifier: ({batch}/{size}) Data: {data:.3f}s | Batch: {bt:.3f}s | | Loss: {loss:.4f} | top1: {top1: .4f} | top5: {top5: .4f}'.format(
                    batch=ind + 1,
                    size=len_t,
                    data=data_time.avg,
                    bt=batch_time.avg,
                    loss=losses.avg,
                    top1=top1.avg,
                    top5=top5.avg,
                    ))

    return (losses.avg, top1.avg)


# In[9]:


def test(test_loader,model,criterion,use_cuda,device=torch.device('cuda'), debug_='MEDIUM',batch_size=64, isAdvReg=0):
    if hasattr(model,'config'):
        batch_size=model.config.structure.bsize
        
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()
    top5 = AverageMeter()

    # switch to evaluate mode
    model.eval()

    end = time.time() 
    

    data_time.update(time.time() - end)
 
    total = 0
    for ind,(inputs,targets) in enumerate(test_loader):
        inputs =  inputs.to(device)
        targets = targets.to(device)
        total += len(inputs) 
        # compute output
        # compute output
        outputs = model(inputs)

        if(type(outputs)==tuple):
            outputs = outputs[0]
        
        loss = criterion(outputs, targets) 
        # measure accuracy and record loss
        prec1, prec5 = accuracy(outputs.data, targets.data, topk=(1, 5))
        losses.update(loss.item(), inputs.size(0))
        top1.update(prec1.item(), inputs.size(0))
        top5.update(prec5.item(), inputs.size(0))

    return (losses.avg, top1.avg)









